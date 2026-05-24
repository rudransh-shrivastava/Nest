import { gql } from '@apollo/client'

export const CREATE_BOARD_CANDIDATE_CLAIM = gql`
  mutation CreateBoardCandidateClaim($input: CreateBoardCandidateClaimInput!) {
    createBoardCandidateClaim(inputData: $input) {
      id
      title
      description
      status
    }
  }
`

export const SUBMIT_BOARD_CANDIDATE_CLAIM = gql`
  mutation SubmitBoardCandidateClaim($input: UpdateBoardCandidateClaimInput!) {
    updateBoardCandidateClaim(inputData: $input) {
      id
      status
    }
  }
`

export const CREATE_BOARD_CANDIDATE_CLAIM_EVIDENCE = gql`
  mutation CreateBoardCandidateClaimEvidence($input: CreateBoardCandidateClaimEvidenceInput!) {
    createBoardCandidateClaimEvidence(inputData: $input) {
      id
      title
      fileName
      fileSize
      sourceUrl
    }
  }
`
