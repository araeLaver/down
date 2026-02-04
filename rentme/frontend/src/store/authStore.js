import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '../api/client'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email, password) => {
        set({ isLoading: true })
        try {
          const response = await api.post('/auth/login', { email, password })
          const { access_token, user } = response.data

          set({
            user,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
          })

          return { success: true }
        } catch (error) {
          set({ isLoading: false })
          return {
            success: false,
            error: error.response?.data?.detail || '로그인에 실패했습니다',
          }
        }
      },

      register: async (userData) => {
        set({ isLoading: true })
        try {
          const response = await api.post('/auth/register', userData)
          const { access_token, user } = response.data

          set({
            user,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
          })

          return { success: true }
        } catch (error) {
          set({ isLoading: false })
          return {
            success: false,
            error: error.response?.data?.detail || '회원가입에 실패했습니다',
          }
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      fetchUser: async () => {
        const token = get().token
        if (!token) return

        try {
          const response = await api.get('/auth/me')
          set({ user: response.data })
        } catch (error) {
          get().logout()
        }
      },
    }),
    {
      name: 'rentme-auth',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
