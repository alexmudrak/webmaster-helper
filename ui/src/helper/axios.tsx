import axios from 'axios'
import createAuthRefreshInterceptor from 'axios-auth-refresh'
import { getRefreshToken, getAccessToken } from '../hooks/user.actions'
import { useHistory } from 'react-router-dom'

const env = import.meta.env
const axiosService = axios.create({
    baseURL: env.VITE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

axiosService.interceptors.request.use(async (config) => {
    config.headers.Authorization = `Bearer ${getAccessToken()}`
    return config
})

axiosService.interceptors.response.use(
    (res) => Promise.resolve(res),
    (err) => Promise.reject(err),
)

const refreshAuthLogic = async (failedRequest) => {
    return axios
        .post(
            '/auth/refresh/',
            {
                refresh: getRefreshToken(),
            },
            {
                baseURL: env.VITE_API_URL,
                headers: {
                    Authorization: `Bearer ${getRefreshToken()}`,
                },
            },
        )
        .then((resp) => {
            let { access, refresh, user } = resp.data
            const old_data = JSON.parse(localStorage.getItem('auth'))
            refresh = old_data.refresh
            user = old_data.user
            failedRequest.response.config.headers['Authorization'] =
                'Bearer ' + access
            localStorage.setItem(
                'auth',
                JSON.stringify({ access, refresh, user }),
            )
        })
        .catch(() => {
            localStorage.removeItem('auth')
            window.location.href = '/'
        })
}

createAuthRefreshInterceptor(axiosService, refreshAuthLogic)

export function fetcher(url: string) {
    return axiosService.get(url).then((res) => res.data)
}
export default axiosService
