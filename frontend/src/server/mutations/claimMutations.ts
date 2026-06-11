import { gql } from '@apollo/client'

export const CREATE_CLAIM = gql`
  mutation CreateBoardCandidateClaim($input: CreateClaimInput!) {
    createBoardCandidateClaim(inputData: $input) {
      ok
      code
      message
    }
  }
`

export const UPDATE_CLAIM = gql`
  mutation UpdateBoardCandidateClaim($input: UpdateClaimInput!) {
    updateBoardCandidateClaim(inputData: $input) {
      ok
      code
      message
    }
  }
`
