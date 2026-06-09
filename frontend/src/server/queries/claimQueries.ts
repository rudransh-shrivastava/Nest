import { gql } from '@apollo/client'

export const GET_CANDIDATE_CLAIMS = gql`
  query GetBoardCandidateClaims($login: String!, $year: Int!) {
    boardCandidateClaims(login: $login, year: $year){
      id
      description
      order
      status
      title
    }
  }
`
