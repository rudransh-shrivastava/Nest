import { gql } from '@apollo/client'

export const CREATE_CLAIM_EVIDENCE = gql`
  mutation CreateBoardCandidateClaimEvidence($input: CreateEvidenceInput!) {
    createBoardCandidateClaimEvidence(inputData: $input) {
      ok
      code
      message
    }
  }
`
