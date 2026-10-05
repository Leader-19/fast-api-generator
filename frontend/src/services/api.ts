import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_API,

    headers: {
        Accept: 'application/json',
    },
})

// console.log(
//     'API Base URL:',
//     import.meta.env.VITE_BACKEND_API,
// )

api.interceptors.request.use(
    (config) => {

        const token =
            localStorage.getItem('token')

        if (token) {
            config.headers.Authorization =
                `Bearer ${token}`
        }

        return config
    },
)

export default api