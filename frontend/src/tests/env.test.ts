import { describe, it, expect } from "vitest"
import { envSchema } from "../env"

describe("Frontend Environment Variable Schema", () => {
  it("should parse valid configurations and apply defaults", () => {
    const parsed = envSchema.parse({
      VITE_API_URL: "https://api.production.com/api/v1",
    })
    expect(parsed.VITE_API_URL).toBe("https://api.production.com/api/v1")
    expect(parsed.VITE_APP_NAME).toBe("AI Semantic Search Engine")
    expect(parsed.VITE_DEFAULT_LANGUAGE).toBe("en")
  })

  it("should throw validation error for invalid URLs", () => {
    const result = envSchema.safeParse({
      VITE_API_URL: "not-a-valid-url",
    })
    expect(result.success).toBe(false)
  })

  it("should apply default configurations when values are missing", () => {
    const parsed = envSchema.parse({})
    expect(parsed.VITE_API_URL).toBe("http://localhost:8000/api/v1")
    expect(parsed.VITE_APP_NAME).toBe("AI Semantic Search Engine")
    expect(parsed.VITE_DEFAULT_LANGUAGE).toBe("en")
  })
})
