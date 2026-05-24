'use client'

import { useQuery, useMutation } from '@apollo/client/react'
import { Button } from '@heroui/button'
import { Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, useDisclosure } from '@heroui/modal'
import { Input, Textarea } from '@heroui/react'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { useParams } from 'next/navigation'
import { useState } from 'react'

import { handleAppError, ErrorDisplay } from 'app/global-error'
import LoadingSpinner from 'components/LoadingSpinner'
import { GET_CANDIDATE_CLAIMS } from 'server/queries/claimQueries'
import { CREATE_BOARD_CANDIDATE_CLAIM } from 'server/mutations/claimMutations'

dayjs.extend(relativeTime)

const ClaimsDashboardPage = () => {
  const { year, login } = useParams<{ year: string; login: string }>()
  const { isOpen, onOpen, onOpenChange } = useDisclosure()

  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  // We pass the candidateId to the query.
  // In the backend query, it expects candidate_id but we mapped it to candidateId in the GraphQL schema probably.
  // Wait, the backend query takes `candidateId` (or `candidate_id` converted to camelCase in strawberry).
  const { data, loading, error, refetch } = useQuery(GET_CANDIDATE_CLAIMS, {
    variables: { year: parseInt(year), login },
    skip: !login,
  })

  const [createClaim, { loading: creating }] = useMutation(CREATE_BOARD_CANDIDATE_CLAIM, {
    onCompleted: () => {
      refetch()
      setTitle('')
      setDescription('')
    },
    onError: (err) => {
      handleAppError(err)
    }
  })

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorDisplay statusCode={500} title="Error" message={error.message} />

  // Fallback data if no claims
  const claims = data?.boardCandidateClaims || []
  const submittedClaims = claims.filter((c: any) => c.status === 'SUBMITTED' || c.status === 'DRAFT')
  const verifiedClaims = claims.filter((c: any) => c.status === 'APPROVED')

  const handleSubmitClaim = async (onClose: () => void) => {
    try {
      await createClaim({
        variables: {
          input: {
            year: parseInt(year),
            login,
            title,
            description,
          }
        }
      })
      onClose()
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Claims — candidate
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Submit claims and evidence for verification. Submissions are disabled in this PoC.
          </p>
        </div>
        <div className="mt-4 md:mt-0">
          <Button color="primary" variant="bordered" onPress={onOpen}>
            + Submit Claim
          </Button>
        </div>
      </div>

      <div className="space-y-8">
        {/* Submitted Claims */}
        <div className="rounded-lg bg-gray-50 dark:bg-gray-800/50 p-6 shadow-sm ring-1 ring-gray-200 dark:ring-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Submitted Claims
          </h2>
          {submittedClaims.length === 0 ? (
            <p className="text-sm text-gray-500">No submitted claims yet.</p>
          ) : (
            <div className="space-y-4">
              {submittedClaims.map((claim: any) => (
                <div key={claim.id} className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-gray-200 dark:border-gray-700 pb-4 last:border-0 last:pb-0">
                  <div>
                    <h3 className="text-md font-bold text-gray-900 dark:text-white">
                      {claim.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {claim.description}
                    </p>
                    <p className="text-xs text-gray-500 mt-2">
                      {dayjs(claim.nestCreatedAt).format('YYYY-MM-DD')}
                    </p>
                  </div>
                  <Button size="sm" variant="light" className="mt-2 sm:mt-0">
                    Details
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Verified Claims */}
        <div className="rounded-lg bg-gray-50 dark:bg-gray-800/50 p-6 shadow-sm ring-1 ring-gray-200 dark:ring-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Verified Claims
          </h2>
          {verifiedClaims.length === 0 ? (
            <p className="text-sm text-gray-500">No verified claims yet.</p>
          ) : (
            <div className="space-y-4">
              {verifiedClaims.map((claim: any) => (
                <div key={claim.id} className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-gray-200 dark:border-gray-700 pb-4 last:border-0 last:pb-0">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-md font-bold text-gray-900 dark:text-white">
                        {claim.title}
                      </h3>
                      <span className="rounded bg-green-100 px-1.5 py-0.5 text-[10px] font-semibold text-green-800 dark:bg-green-800/40 dark:text-green-300">
                        Verified
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {claim.description}
                    </p>
                    <p className="text-xs text-gray-500 mt-2">
                      {dayjs(claim.nestCreatedAt).format('YYYY-MM-DD')}
                    </p>
                  </div>
                  <Button size="sm" variant="light" className="mt-2 sm:mt-0">
                    Details
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">Submit New Claim</ModalHeader>
              <ModalBody>
                <p className="text-sm text-gray-500 mb-4">
                  Provide verifiable details about your contributions, leadership roles, or credentials.
                </p>
                <Input
                  label="Title"
                  placeholder="e.g. OWASP Chapter Chair"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  isRequired
                />
                <Textarea
                  label="Description"
                  placeholder="Describe your role and impact..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="mt-4"
                  isRequired
                />
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Cancel
                </Button>
                <Button color="primary" onPress={() => handleSubmitClaim(onClose)} isLoading={creating}>
                  Submit
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  )
}

export default ClaimsDashboardPage
