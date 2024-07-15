import polyglotI18nProvider from "ra-i18n-polyglot"
import raEnglishMessages from "ra-language-english"
import raRussianMessages from "ra-language-russian"
import { resolveBrowserLocale } from "react-admin"
import muffinEnglishMessages from "./en"
import muffinRussianMessages from "./ru"

const translations = {
  en: { ...raEnglishMessages, ...muffinEnglishMessages },
  ru: { ...raRussianMessages, ...muffinRussianMessages },
}

export const muffinI18nProvider = polyglotI18nProvider(
  (locale) => (translations[locale] ? translations[locale] : translations.en),
  resolveBrowserLocale(),
  [
    { locale: "en", name: "English" },
    { locale: "ru", name: "Русский" },
  ],
  { allowMissing: true }
)
