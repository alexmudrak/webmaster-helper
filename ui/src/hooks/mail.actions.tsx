import axiosService from '../helper/axios'

function useMailActions() {
  const runMailCollectors = async () => {
    try {
      const response = await axiosService.post(`/mails/run-get-mails/`)
      console.log(`Run Mail Collectors successfully`)
      return response.data
    } catch (error) {
      console.error(`Error running Mail Collectors:`, error)
    }
  }

  return { runMailCollectors }
}

export { useMailActions }
