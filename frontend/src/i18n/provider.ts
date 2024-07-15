import polyglotI18nProvider from "ra-i18n-polyglot"
import { resolveBrowserLocale } from "react-admin"
import muffinEnglishMessages from "./en"
import muffinRussianMessages from "./ru"

export const muffinTranslations = {
  en: muffinEnglishMessages,
  ru: muffinRussianMessages,
}

const defaultLocale = "en"

export const buildProvider = (translations) => {
  return polyglotI18nProvider(
    (locale) => (translations[locale] ? translations[locale] : translations[defaultLocale]),
    resolveBrowserLocale(),
    [
      { locale: "en", name: "English" },
      { locale: "ru", name: "Русский" },
    ],
    { allowMissing: true }
  )
}
