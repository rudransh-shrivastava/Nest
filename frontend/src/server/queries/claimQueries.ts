import { gql } from '@apollo/client'

export const GET_CANDIDATE_CLAIM = gql`
  query GetBoardCandidateClaim($login: String!, $key: String!) {
    boardCandidateClaim(login: $login, key: $key) {
      id
      description
      key
      name
      status
      updatedAt
    }
  }
`

export const GET_CANDIDATE_CLAIMS = gql`
  query GetBoardCandidateClaims($login: String!, $year: Int!) {
    boardCandidateClaims(login: $login, year: $year) {
      id
      description
      key
      name
      order
      status
    }
  }
`
