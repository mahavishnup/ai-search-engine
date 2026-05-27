import { z } from "zod"

export const envSchema = z.object({
  VITE_API_URL: z.string().url().default("http://localhost:8000/api/v1"),
  VITE_APP_NAME: z.string().default("AI Semantic Search Engine"),
  VITE_DEFAULT_LANGUAGE: z.enum(["en"]).default("en"),
})

export const env = envSchema.parse(import.meta.env)
