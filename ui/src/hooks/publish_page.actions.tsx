import axiosService from '../helper/axios'

function usePublishPageActions() {
  const deleteItem = async (itemId: string) => {
    try {
      await axiosService.delete(`/publish-pages/${itemId}/`)
      console.log(`Publish Page with id ${itemId} deleted successfully`)
    } catch (error) {
      console.error(`Error deleting Publish Page with id ${itemId}:`, error)
    }
  }

  return { deleteItem }
}

export { usePublishPageActions }
