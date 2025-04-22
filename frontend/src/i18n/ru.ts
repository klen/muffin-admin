import { TranslationMessages } from "ra-core"
import raRussianMessages from "ra-language-russian"

const muffinRussianMessages = {
  ...raRussianMessages,
  muffin: {
    instructions: "Инструкции",
    how_to_use_admin: "Как использовать админку?",
    action: {
      search: "Enter для поиска",
    },
  },
} as unknown as TranslationMessages

muffinRussianMessages.ra.action.edit = "Изменить"

export default muffinRussianMessages
