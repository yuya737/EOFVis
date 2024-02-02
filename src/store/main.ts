import { defineStore } from 'pinia'

// You can name the return value of `defineStore()` anything you want,
// but it's best to use the name of the store and surround it with `use`
// and `Store` (e.g. `useUserStore`, `useCartStore`, `useProductStore`)
// the first argument is a unique id of the store across your application
export const useStore = defineStore('main', {
  // other options...
  state: () => {
    return {
        // model_id id
        model_id: '',
        // ensemble_id id
        ensemble_id: '',
    }

  },
  getters: {
    getID(){
        return {model_id: this.model_id, ensemble_id: this.ensemble_id }
    }
  },
  actions: {
    updateID(model_id: string, ensemble_id: string){
        this.model_id = model_id
        this.ensemble_id = ensemble_id
    }

  }
})
