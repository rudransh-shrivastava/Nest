'use client'

import { useQuery } from '@apollo/client/react'
import { Button } from '@heroui/button'
import { useDjangoSession } from 'hooks/useDjangoSession'
import { useParams, useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { FaPlus } from 'react-icons/fa6'
import { handleAppError } from 'app/global-error'
import { GetBoardCandidateDocument } from 'types/__generated__/boardQueries.generated'
import { GetBoardCandidateClaimsDocument } from 'types/__generated__/claimQueries.generated'
import { formatDate } from 'utils/dateFormatter'
import AccessDeniedDisplay from 'components/AccessDeniedDisplay'
import ActionButton from 'components/ActionButton'
import LoadingSpinner from 'components/LoadingSpinner'
import SecondaryCard from 'components/SecondaryCard'

const CandidateClaimsPage = () => {
  const router = useRouter()
  const { isSyncing, session } = useDjangoSession()
  const { login, year } = useParams<{ login: string; year: string }>()

  const {
    data: graphQLData,
    error: graphQLRequestError,
    loading: isLoading,
  } = useQuery(GetBoardCandidateClaimsDocument, {
    skip: !login || !year,
    variables: { login: login, year: Number.parseInt(year) },
  })

  const { data: candidateGraphQLData } = useQuery(GetBoardCandidateDocument, {
    variables: { login: login, year: Number.parseInt(year) },
  })

  const isCandidate = candidateGraphQLData?.boardOfDirectors?.candidate != null

  useEffect(() => {
    if (graphQLRequestError) {
      handleAppError(graphQLRequestError)
    }
  }, [graphQLRequestError])

  if (isSyncing || isLoading) {
    return <LoadingSpinner />
  }

  if (!isCandidate || session?.user?.login !== login) {
    return (
      <AccessDeniedDisplay title="Access Denied" message="You can only view your own claims." />
    )
  }

  const handleCreate = () => router.push(`/board/${year}/candidates/${login}/claims/create`)
  const handleClaimClick = (key: string) =>
    router.push(`/board/${year}/candidates/${login}/claims/${key}`)

  const claims = graphQLData?.boardCandidateClaims ?? []
  const sectionConfig = [
    { title: 'Draft Claims', items: claims.filter((c) => c.status === 'DRAFT') },
    { title: 'Submitted Claims', items: claims.filter((c) => c.status === 'SUBMITTED') },
    { title: 'Approved Claims', items: claims.filter((c) => c.status === 'APPROVED') },
    { title: 'Rejected Claims', items: claims.filter((c) => c.status === 'REJECTED') },
    { title: 'Withdrawn Claims', items: claims.filter((c) => c.status === 'WITHDRAWN') },
  ]

  return (
    <div className="container mx-auto px-4 py-8 dark:bg-[#212529]">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-600 dark:text-white">Claims</h1>
          <p className="text-gray-600 dark:text-gray-400">Claims you've created</p>
        </div>
        <ActionButton onClick={handleCreate}>
          <FaPlus className="mr-2" />
          {'Create Claim'}
        </ActionButton>
      </div>
      {sectionConfig.map(({ title, items }) => (
        <SecondaryCard key={title} title={title}>
          {items.length == 0 ? (
            <p> No {title.toLowerCase()}. </p>
          ) : (
            <div className="grid gap-2">
              {items.map((claim) => (
                <Button
                  key={claim.key}
                  onPress={() => handleClaimClick(claim.key)}
                  className="h-28 flex-col items-start justify-start bg-transparent p-4 dark:hover:bg-gray-900"
                >
                  <h3 className="w-full min-w-0 truncate text-left text-xl leading-tight font-semibold dark:text-gray-300">
                    {claim.name}
                  </h3>
                  <p className="w-full min-w-0 truncate text-left leading-tight text-gray-600 dark:text-gray-300">
                    {claim.description}
                  </p>
                  <span className="shrink-0 text-xs text-gray-600 dark:text-gray-400">
                    {formatDate(claim.createdAt)}
                  </span>
                </Button>
              ))}
            </div>
          )}
        </SecondaryCard>
      ))}
    </div>
  )
}

export default CandidateClaimsPage
