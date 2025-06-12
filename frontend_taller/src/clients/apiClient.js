import axios from 'axios'

const instance = axios.create({
  baseURL: 'https://tu-api.com/api', // cambia esto a la URL real
  timeout: 5000
})

export default instance 