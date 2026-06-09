'use client'

import { useParams } from 'next/navigation'
import { useDjangoSession } from 'hooks/useDjangoSession'
import AccessDeniedDisplay from 'components/AccessDeniedDisplay'
import LoadingSpinner from 'components/LoadingSpinner'
import ActionButton from 'components/ActionButton'
import { FaPlus } from 'react-icons/fa6'
import { useQuery } from '@apollo/client/react'
import { GetBoardCandidateClaimsDocument } from 'types/__generated__/claimQueries.generated'
import { useEffect } from 'react'
import { handleAppError } from 'app/global-error'
import SecondaryCard from 'components/SecondaryCard'

const CandidateClaimsPage = () => {
  const { isSyncing, session } = useDjangoSession()
  const { login, year } = useParams<{ login: string, year: string }>()

  const {
    data: graphQLData,
    error: graphQLRequestError,
    loading: isLoading,
  } = useQuery(GetBoardCandidateClaimsDocument, {
    variables: { login: login, year: Number.parseInt(year) },
  })

  useEffect(() => {
    if (graphQLRequestError) {
      handleAppError(graphQLRequestError)
    }
  }, [graphQLRequestError])

  if (isSyncing || isLoading) {
    return <LoadingSpinner />
  }

  if (session?.user?.login !== login) {
    return (
      <AccessDeniedDisplay
        title="Access Denied"
        message="You can only view your own candidate claims."
      />
    )
  }

  const claims = graphQLData?.boardCandidateClaims ?? []

  const draftClaims = claims.filter((c) => c.status === 'DRAFT')
  const submittedClaims = claims.filter((c) => c.status === 'SUBMITTED')
  const approvedClaims = claims.filter((c) => c.status === 'APPROVED')
  const rejectedClaims = claims.filter((c) => c.status === 'REJECTED')
  const withdrawnClaims = claims.filter((c) => c.status === 'WITHDRAWN')

  const sectionConfig = [
    { title: "Draft Claims", items: draftClaims },
    { title: "Submitted Claims", items: submittedClaims },
    { title: "Approved Claims", items: approvedClaims },
    { title: "Rejected Claims", items: rejectedClaims },
    { title: "Withdrawn Claims", items: withdrawnClaims },
  ]

  return (
    <div className="container mx-auto px-4 py-8 dark:bg-[#212529]">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-600 dark:text-white">Claims</h1>
          <p className="text-gray-600 dark:text-gray-400">Claims you've created</p>
        </div>
        <ActionButton>
          <FaPlus className="mr-2" />
          {'Create Claim'}
        </ActionButton>
      </div>
      {sectionConfig.map(({ title, items }) => (
        <SecondaryCard title={title}>
          {items.length == 0 ? (
            <p> No {title.toLowerCase()}. </p>
          ) : (
            <div className="grid gap-4">
              {items.map((claim) => (
                <div key={claim.title} className="rounded-lg bg-gray-200 p-4 dark:bg-gray-700">
                  <h3 className="mb-2 text-lg font-semibold text-blue-400">{claim.title}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{claim.description}</p>
                </div>
              ))
              }
            </div >
          )}
        </SecondaryCard>
      ))}
    </div >
  )
}

export default CandidateClaimsPage
