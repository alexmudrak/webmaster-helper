import axiosService from '../helper/axios'

function useWebsiteActions() {
  const getWebsites = async () => {
    try {
      const response = await axiosService.get(`/url/`)
      console.log(`Get Websites successfully`)
      return response.data?.results
    } catch (error) {
      console.error(`Error getting Websites:`, error)
    }
  }
  const deleteWebsiteItem = async (itemId: string) => {
    try {
      await axiosService.delete(`/url/${itemId}/`)
      console.log(`Website with id ${itemId} deleted successfully`)
    } catch (error) {
      console.error(`Error deleting Website with id ${itemId}:`, error)
    }
  }

  return { deleteWebsiteItem, getWebsites }
}

export { useWebsiteActions }
