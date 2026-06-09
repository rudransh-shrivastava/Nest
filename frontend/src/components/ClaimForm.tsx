'use client'

import type React from 'react'
import { useState } from 'react'
import { extractGraphQLErrors } from 'utils/helpers/handleGraphQLError'
import { FormButtons } from 'components/forms/shared/FormButtons'
import { FormContainer } from 'components/forms/shared/FormContainer'
import { FormTextarea } from 'components/forms/shared/FormTextarea'
import { FormTextInput } from 'components/forms/shared/FormTextInput'
import {
  validateDescription,
  validateTitle,
} from 'components/forms/shared/formValidationUtils'
import { useFormValidation } from './forms/shared/useFormValidation'

interface ClaimFormProps {
  formData: {
    description: string
    title: string
  }
  setFormData: React.Dispatch<
    React.SetStateAction<{
      description: string
      title: string
    }>
  >
  onSubmit: (e: React.FormEvent) => Promise<void>
  loading: boolean
  title: string
  submitText?: string
  isEdit?: boolean
}

const ClaimForm = ({
  formData,
  setFormData,
  onSubmit,
  loading,
  title,
  isEdit,
  submitText = 'Create Claim',
}: ClaimFormProps) => {
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  const [backendErrors, setBackendErrors] = useState<Record<string, string>>({})

  const handleInputChange = (name: string, value: string | number) => {
    setFormData((prev) => ({ ...prev, [name]: value }))
    if (backendErrors[name]) {
      setBackendErrors((prev) => {
        const next = { ...prev }
        delete next[name]
        return next
      })
    }
  }

  const errors = useFormValidation(
    [
      {
        field: 'description',
        shouldValidate: touched.description ?? false,
        validator: () => validateDescription(formData.description),
      },
      {
        field: 'title',
        shouldValidate: touched.title ?? false,
        validator: () => validateTitle(formData.title),
      },
    ],
    [formData, touched, backendErrors]
  )

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const allFields = ['description', 'title']
    const newTouched: Record<string, boolean> = {}
    allFields.forEach((field) => {
      newTouched[field] = true
    })
    setTouched(newTouched)

    const descriptionError = validateDescription(formData.description)
    const titleError = validateTitle(formData.title)

    // Prevent submission if any validation errors exist
    if (descriptionError || titleError) {
      return
    }

    try {
      await onSubmit(e)
    } catch (error) {
      const { validationErrors, hasValidationErrors } = extractGraphQLErrors(error)
      if (hasValidationErrors) {
        setBackendErrors(validationErrors)
      }
    }
  }

  return (
    <FormContainer
      title={title}
      onSubmit={handleSubmit}
      containerClassName="claim-form-container"
    >
      {/* Basic Information */}
      <section className="flex flex-col gap-6">
        <div className="grid grid-cols-1 gap-6 text-gray-600 lg:grid-cols-2 dark:text-gray-300">
          <FormTextInput
            id="claim-title"
            label="Title"
            placeholder="Enter claim title"
            value={formData.title}
            onValueChange={(value) => {
              handleInputChange('title', value)
              setTouched((prev) => ({ ...prev, title: true }))
            }}
            error={errors.title}
            touched={touched.title}
            required
            className="w-full min-w-0 lg:col-span-2"
          />

          <FormTextarea
            id="claim-description"
            label="Description"
            placeholder="Enter claim description"
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            error={errors.description}
            touched={touched.description}
            required
          />
        </div>
      </section>
      <FormButtons loading={loading} submitText={submitText} />
    </FormContainer>
  )
}

export default ClaimForm
