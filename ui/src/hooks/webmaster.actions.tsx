import axiosService from '../helper/axios'

// TODO: Add typescript
function useWebmastersActions() {
  const getWebmasters = async () => {
    try {
      const response = await axiosService.get(`/webmaster/`)
      console.log(`Get Webmasters successfully`)
      return response.data?.results
    } catch (error) {
      console.error(`Error getting Webmasters:`, error)
    }
  }

  const deleteWebmastersItem = async (itemId: string) => {
    try {
      await axiosService.delete(`/webmaster/${itemId}/`)
      console.log(`Webmaster with id ${itemId} deleted successfully`)
    } catch (error) {
      console.error(`Error deleting Webmaster with id ${itemId}:`, error)
    }
  }

  return { getWebmasters, deleteWebmastersItem }
}

export { useWebmastersActions }
