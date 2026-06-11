'use client'
import { useMutation, useQuery } from '@apollo/client/react'
import { addToast } from '@heroui/toast'
import { useDjangoSession } from 'hooks/useDjangoSession'
import { useParams, useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import { ErrorDisplay, handleAppError } from 'app/global-error'
import { UpdateBoardCandidateClaimDocument } from 'types/__generated__/claimMutations.generated'
import { GetBoardCandidateClaimDocument } from 'types/__generated__/claimQueries.generated'
import { extractGraphQLErrors } from 'utils/helpers/handleGraphQLError'
import slugify from 'utils/slugify'
import AccessDeniedDisplay from 'components/AccessDeniedDisplay'
import ClaimForm from 'components/ClaimForm'
import LoadingSpinner from 'components/LoadingSpinner'

const EditClaimPage = () => {
  const router = useRouter()
  const { claimKey, login, year } = useParams<{ claimKey: string; login: string; year: string }>()
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

  const [updateClaim, { loading }] = useMutation(UpdateBoardCandidateClaimDocument)
  const [formData, setFormData] = useState({
    description: '',
    key: '',
    name: '',
  })

  useEffect(() => {
    if (graphQLRequestError) {
      handleAppError(graphQLRequestError)
    }
  }, [graphQLRequestError])

  const claim = graphQLData?.boardCandidateClaim

  useEffect(() => {
    if (claim) {
      setFormData({
        description: claim.description ?? '',
        key: claim.key ?? '',
        name: claim.name ?? '',
      })
    }
  }, [claim])

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
      <AccessDeniedDisplay title="Access Denied" message="You can only view your own claims." />
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const input = {
        description: formData.description,
        key: formData.key,
        name: formData.name,
      }

      await updateClaim({
        awaitRefetchQueries: true,
        refetchQueries: [
          {
            query: GetBoardCandidateClaimDocument,
            variables: { key: claimKey, login },
          },
        ],
        variables: { input },
      })

      addToast({
        description: 'Claim updated successfully!',
        title: 'Success',
        timeout: 3000,
        shouldShowTimeoutProgress: true,
        color: 'success',
        variant: 'solid',
      })

      router.push(`/board/${year}/candidates/${login}/claims/${slugify(formData.name)}`)
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
      title="Edit Claim"
    />
  )
}

export default EditClaimPage
