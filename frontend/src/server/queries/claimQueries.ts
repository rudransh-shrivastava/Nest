import { gql } from '@apollo/client'

export const GET_CANDIDATE_CLAIMS = gql`
  query GetCandidateClaims($year: Int!, $login: String!) {
    boardCandidateClaims(year: $year, login: $login) {
      id
      title
      description
      status
      isLocked
      nestCreatedAt
      nestUpdatedAt
      withdrawnReason
      withdrawnAt
      evidences {
        id
        title
        description
        fileName
        fileSize
        sourceUrl
      }
    }
  }
`
