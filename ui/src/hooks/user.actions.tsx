import axios from 'axios'
import { useNavigate } from 'react-router-dom'

import axiosService from '../helper/axios'
import { UserLocalData, UserLoginData, UserRegisterData } from '../types'

function useUserActions() {
  const baseURL = import.meta.env.VITE_API_URL
  const navigate = useNavigate()

  function login(data: UserLoginData) {
    return axios.post(`${baseURL}/auth/login/`, data).then((res) => {
      setUserData(res.data)
      navigate('/')
    })
  }

  function register(data: UserRegisterData) {
    return axios.post(`${baseURL}/auth/register/`, data).then((res) => {
      setUserData(res.data)
      navigate('/')
    })
  }

  function logout() {
    return axiosService
      .post(`${baseURL}/auth/logout/`, {
        refresh: getRefreshToken()
      })
      .then(() => {
        localStorage.removeItem('auth')
        navigate('/login')
      })
  }

  return { login, register, logout }
}

function getFromLocalStorage(key: string) {
  const authJSON = localStorage.getItem('auth')
  if (authJSON !== null) {
    const auth = JSON.parse(authJSON)
    return auth[key] || null
  }
  return null
}

function setUserData(data: UserLocalData) {
  localStorage.setItem(
    'auth',
    JSON.stringify({
      access: data.access,
      refresh: data.refresh,
      user: data.user
    })
  )
}

const getAccessToken = () => {
  return getFromLocalStorage('access')
}
const getRefreshToken = () => {
  return getFromLocalStorage('refresh')
}
const getUser = () => {
  return getFromLocalStorage('user')
}

export {
  getAccessToken,
  getRefreshToken,
  getUser,
  setUserData,
  useUserActions
}
