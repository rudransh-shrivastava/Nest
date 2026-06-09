'use client'
import { useMutation } from '@apollo/client/react'
import { addToast } from '@heroui/toast'
import { useParams, useRouter } from 'next/navigation'
import React, { useState } from 'react'

import { extractGraphQLErrors } from 'utils/helpers/handleGraphQLError'
import LoadingSpinner from 'components/LoadingSpinner'
import { CreateBoardCandidateClaimDocument } from 'types/__generated__/claimMutations.generated'
import AccessDeniedDisplay from 'components/AccessDeniedDisplay'
import { GetBoardCandidateClaimsDocument } from 'types/__generated__/claimQueries.generated'
import { useDjangoSession } from 'hooks/useDjangoSession'
import ClaimForm from 'components/ClaimForm'

const CreateClaimPage = () => {
  const router = useRouter()
  const isCandidate = true // TODO: fetch this from backend instead -> a graphql query
  const { isSyncing, session } = useDjangoSession()
  const { login, year } = useParams<{ login: string, year: string }>()

  const [createClaim, { loading }] = useMutation(CreateBoardCandidateClaimDocument)

  const [formData, setFormData] = useState({
    description: '',
    title: '',
  })

  if (!isCandidate || session?.user?.login !== login) {
    return (
      <AccessDeniedDisplay
        title="Access Denied"
        message="You must be a candiadte to create a claim."
      />
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const input = {
        title: formData.title,
        description: formData.description,
        year: Number.parseInt(year),
      }

      await createClaim({
        awaitRefetchQueries: true,
        refetchQueries: [{
          query: GetBoardCandidateClaimsDocument,
          variables: { login, year: Number.parseInt(year) }
        }],
        variables: { input },
      })

      addToast({
        description: 'Claim created successfully!',
        title: 'Success',
        timeout: 3000,
        shouldShowTimeoutProgress: true,
        color: 'success',
        variant: 'solid',
      })

      router.push(`/board/${year}/candidates/${login}/claims`)
    } catch (err) {
      // TODO: handle validation errors inline using setValidationErrors + extractGraphQLErrors
      const { hasValidationErrors } = extractGraphQLErrors(err)
      if (!hasValidationErrors) {
        addToast({
          description:
            err instanceof Error ? err.message : 'Unable to complete the requested operation.',
          title: 'GraphQL Request Failed',
          timeout: 3000,
          shouldShowTimeoutProgress: true,
          color: 'danger',
          variant: 'solid',
        })
      }
      throw err
    }
  }

  if (isSyncing) {
    return <LoadingSpinner />
  }

  return (
    <ClaimForm
      formData={formData}
      setFormData={setFormData}
      onSubmit={handleSubmit}
      loading={loading}
      title="Create Claim"
      isEdit={false}
    />
  )
}

export default CreateClaimPage
