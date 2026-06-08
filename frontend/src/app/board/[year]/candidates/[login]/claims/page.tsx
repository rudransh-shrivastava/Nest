'use client'

import { useParams } from 'next/navigation'
import { useDjangoSession } from 'hooks/useDjangoSession'
import AccessDeniedDisplay from 'components/AccessDeniedDisplay'
import LoadingSpinner from 'components/LoadingSpinner'
import ActionButton from 'components/ActionButton'
import { FaPlus } from 'react-icons/fa6'

const CandidateClaimsPage = () => {
  const params = useParams()
  const { isSyncing, session } = useDjangoSession()
  const login = params.login as string

  if (isSyncing) {
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
    </div>
  )
}

export default CandidateClaimsPage
