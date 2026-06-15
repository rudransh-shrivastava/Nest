import * as Types from './graphql';

import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type CreateBoardCandidateClaimEvidenceMutationVariables = Types.Exact<{
  input: Types.CreateEvidenceInput;
}>;


export type CreateBoardCandidateClaimEvidenceMutation = { createBoardCandidateClaimEvidence: { __typename: 'EvidenceResult', ok: boolean, code: string | null, message: string | null } };

export type RemoveBoardCandidateClaimEvidenceMutationVariables = Types.Exact<{
  input: Types.RemoveEvidenceInput;
}>;


export type RemoveBoardCandidateClaimEvidenceMutation = { removeBoardCandidateClaimEvidence: { __typename: 'EvidenceResult', ok: boolean, code: string | null, message: string | null } };

export type UpdateBoardCandidateClaimEvidenceMutationVariables = Types.Exact<{
  input: Types.UpdateEvidenceInput;
}>;


export type UpdateBoardCandidateClaimEvidenceMutation = { updateBoardCandidateClaimEvidence: { __typename: 'EvidenceResult', ok: boolean, code: string | null, message: string | null } };


export const CreateBoardCandidateClaimEvidenceDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"CreateBoardCandidateClaimEvidence"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"CreateEvidenceInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"createBoardCandidateClaimEvidence"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"inputData"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"ok"}},{"kind":"Field","name":{"kind":"Name","value":"code"}},{"kind":"Field","name":{"kind":"Name","value":"message"}}]}}]}}]} as unknown as DocumentNode<CreateBoardCandidateClaimEvidenceMutation, CreateBoardCandidateClaimEvidenceMutationVariables>;
export const RemoveBoardCandidateClaimEvidenceDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"RemoveBoardCandidateClaimEvidence"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"RemoveEvidenceInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"removeBoardCandidateClaimEvidence"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"inputData"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"ok"}},{"kind":"Field","name":{"kind":"Name","value":"code"}},{"kind":"Field","name":{"kind":"Name","value":"message"}}]}}]}}]} as unknown as DocumentNode<RemoveBoardCandidateClaimEvidenceMutation, RemoveBoardCandidateClaimEvidenceMutationVariables>;
export const UpdateBoardCandidateClaimEvidenceDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"UpdateBoardCandidateClaimEvidence"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"input"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UpdateEvidenceInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"updateBoardCandidateClaimEvidence"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"inputData"},"value":{"kind":"Variable","name":{"kind":"Name","value":"input"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"ok"}},{"kind":"Field","name":{"kind":"Name","value":"code"}},{"kind":"Field","name":{"kind":"Name","value":"message"}}]}}]}}]} as unknown as DocumentNode<UpdateBoardCandidateClaimEvidenceMutation, UpdateBoardCandidateClaimEvidenceMutationVariables>;