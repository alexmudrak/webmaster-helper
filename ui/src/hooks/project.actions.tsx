import axiosService from '../helper/axios'

// TODO: Add typesript
function useProjectActions() {
  const getProjects = async () => {
    try {
      const response = await axiosService.get(`/project/`)
      console.log(`Get Projects successfully`)
      return response.data?.results
    } catch (error) {
      console.error(`Error getting Projects:`, error)
    }
  }
  const deleteProjectItem = async (itemId: string) => {
    try {
      await axiosService.delete(`/project/${itemId}/`)
      console.log(`Project with id ${itemId} deleted successfully`)
    } catch (error) {
      console.error(`Error deleting Project with id ${itemId}:`, error)
    }
  }

  return { deleteProjectItem, getProjects }
}

export { useProjectActions }
