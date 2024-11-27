import { TranslationMessages } from "ra-core"
import raRussianMessages from "ra-language-russian"

const muffinRussianMessages = {
  ...raRussianMessages,
  muffin: {
    instructions: "Инструкции",
    how_to_use_admin: "Как использовать админку?",
  },
} as unknown as TranslationMessages

export default muffinRussianMessages
