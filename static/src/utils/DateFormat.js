const DISPLAY_FORMAT = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }
const DISPLAY_EMAIL_FORMAT = { year: 'numeric', month: '2-digit', day: '2-digit' }
const LOCALE = 'fr-FR'

export default function (value) {
  if (value) {
    const date = new Date(value)
    return date.toLocaleDateString(LOCALE, DISPLAY_FORMAT)
  }
}

export const toBackendFormat = (value) => {
  if (value) {
    const date = new Date(value)
    const day = date.getDate()
    const month = date.getMonth() + 1
    const year = date.getFullYear()
    return `${year}-${month}-${day}`
  }
}

/**
 * Format Date to jj-mm-aaaa
 * @param {*} value
 * @returns
 */
export const toEmailFormat = (value) => {
  if (value) {
    const date = new Date(value)
    return date.toLocaleDateString(LOCALE, DISPLAY_EMAIL_FORMAT).replaceAll('/', '-')
  }
}

export const nowTimeString = () => {
  return new Date().toLocaleTimeString(LOCALE)
}
