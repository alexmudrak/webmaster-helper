import axiosService from '../helper/axios'

function usePaymentActions() {
  const getPayments = async () => {
    try {
      const response = await axiosService.get(`/payment/`)
      console.log(`Get Payments successfully`)
      return response.data?.results
    } catch (error) {
      console.error(`Error getting Payments:`, error)
    }
  }
  const deletePaymentItem = async (itemId: string) => {
    try {
      await axiosService.delete(`/payment/${itemId}/`)
      console.log(`Payment with id ${itemId} deleted successfully`)
    } catch (error) {
      console.error(`Error deleting Payment with id ${itemId}:`, error)
    }
  }

  return { deletePaymentItem, getPayments }
}

export { usePaymentActions }
