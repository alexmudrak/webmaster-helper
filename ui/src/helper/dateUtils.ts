export function formatDate(dateString: string | null | undefined): string {
  try {
    if (dateString === null) {
      return '-'
    }
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }

    const date = new Date(dateString)

    if (isNaN(date.getTime())) {
      return '-'
    }
    return date.toLocaleDateString(undefined, options)
  } catch (error) {
    return '-'
  }
}
