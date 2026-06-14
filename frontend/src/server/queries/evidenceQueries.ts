import { gql } from '@apollo/client'

export const GET_CLAIM_EVIDENCES = gql`
  query GetBoardCandidateClaimEvidences($login: String!, $claimKey: String!, $year: Int!) {
    boardCandidateClaimEvidences(login: $login, claimKey: $claimKey, year: $year) {
      id
      createdAt
      description
      key
      name
      sourceUrl
      updatedAt
    }
  }
`

export const GET_CLAIM_EVIDENCE = gql`
  query GetBoardCandidateClaimEvidence(
    $login: String!
    $claim_key: String!
    $key: String!
    $year: Int!
  ) {
    boardCandidateClaimEvidence(login: $login, claimKey: $claim_key, key: $key, year: $year) {
      id
      createdAt
      description
      key
      name
      sourceUrl
      updatedAt
    }
  }
`
