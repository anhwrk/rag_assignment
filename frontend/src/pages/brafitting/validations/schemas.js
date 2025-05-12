import { z } from 'zod';

export const measurementSchema = z.object({
  message: z.string()
    .min(10, 'Please provide more details about your measurements')
    .max(500, 'Message is too long')
    .refine(
      (value) => /\d+/.test(value),
      'Please include your measurements (numbers)'
    )
    .refine(
      (value) => /(underbust|bust|band|cup)/i.test(value),
      'Please mention bust or underbust measurements'
    )
});

// You can add more schemas here as needed
export const errorMessages = {
  tooShort: 'Please provide more details about your measurements',
  tooLong: 'Message is too long',
  noMeasurements: 'Please include your measurements (numbers)',
  noBustMention: 'Please mention bust or underbust measurements'
}; 