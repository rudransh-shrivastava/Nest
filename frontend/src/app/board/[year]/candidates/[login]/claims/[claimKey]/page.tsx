'use client'

import { useQuery } from '@apollo/client/react'
import { useParams, useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { ErrorDisplay, handleAppError } from 'app/global-error'

import LoadingSpinner from 'components/LoadingSpinner'
import { GetBoardCandidateClaimDocument } from 'types/__generated__/claimQueries.generated'
import { titleCaseWord } from 'utils/capitalize'
import { formatDate } from 'utils/dateFormatter'
import { BreadcrumbStyleProvider } from 'contexts/BreadcrumbContext'
import { useDjangoSession } from 'hooks/useDjangoSession'
import AccessDeniedDisplay from 'components/AccessDeniedDisplay'
import PageWrapper from 'components/cards/PageWrapper'
import Metadata from 'components/cards/Metadata'
import DropdownActions from 'components/DropdownActions'

const ClaimDetailsPage = () => {
  const router = useRouter()
  const { claimKey, login, year } = useParams<{ claimKey: string, login: string, year: string }>()
  const { isSyncing, session } = useDjangoSession()
  const {
    data: graphQLData,
    error: graphQLRequestError,
    loading: isLoading,
  } = useQuery(GetBoardCandidateClaimDocument, {
    fetchPolicy: 'cache-and-network',
    skip: !claimKey,
    variables: { key: claimKey, login: login },
  })

  const claim = graphQLData?.boardCandidateClaim

  useEffect(() => {
    if (graphQLRequestError) {
      handleAppError(graphQLRequestError)
    }
  }, [graphQLRequestError])

  if (isLoading || isSyncing) return <LoadingSpinner />

  if (graphQLRequestError) {
    return (
      <ErrorDisplay
        statusCode={500}
        title="Error loading program"
        message="An error occurred while loading the claim data"
      />
    )
  }

  if (!graphQLData || !claim) {
    return (
      <ErrorDisplay
        statusCode={404}
        title="Claim Not Found"
        message="Sorry, the claim you're looking for doesn't exist."
      />
    )
  }

  if (session?.user?.login !== login) {
    return (
      <AccessDeniedDisplay
        title="Access Denied"
        message="You can only view your own claims."
      />
    )
  }

  const programDetails = [
    { label: 'Name', value: titleCaseWord(claim.name) },
    { label: 'Description', value: claim.description },
    { label: 'Status', value: claim.status },
    { label: 'Last Updated', value: formatDate(claim.updatedAt) },
  ]

  return (
    <BreadcrumbStyleProvider className="bg-white dark:bg-[#212529]">
      <PageWrapper>
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-600 dark:text-white">Claim</h1>
          </div>
          <DropdownActions
            options={[
              {
                key: 'edit',
                label: 'Edit Claim',
                onAction: () =>
                  router.push(`/board/${year}/candidates/${login}/claims/${claimKey}/edit`),
              },
            ]}
          />
        </div>
        <Metadata details={programDetails} detailsTitle="Claim Details" />
      </PageWrapper>
    </BreadcrumbStyleProvider>
  )
}

export default ClaimDetailsPage
