import axiosService from '../helper/axios'

function useContactActions() {
  const getContacts = async () => {
    try {
      const response = await axiosService.get(`/contact/`)
      console.log(`Get Contacts successfully`)
      return response.data?.results
    } catch (error) {
      console.error(`Error getting Contacts:`, error)
    }
  }
  const deleteContactItem = async (itemId: string) => {
    try {
      await axiosService.delete(`/contact/${itemId}/`)
      console.log(`Contact with id ${itemId} deleted successfully`)
    } catch (error) {
      console.error(`Error deleting Contact with id ${itemId}:`, error)
    }
  }

  return { deleteContactItem, getContacts }
}

export { useContactActions }
