import { defineStore } from "pinia";

// You can name the return value of `defineStore()` anything you want,
// but it's best to use the name of the store and surround it with `use`
// and `Store` (e.g. `useUserStore`, `useCartStore`, `useProductStore`)
// the first argument is a unique id of the store across your application
export const useStore = defineStore("main", {
    // other options...
    state: () => {
        return {
            // file_name
            file_name: "",

            name: "",
        };
    },
    getters: {
        getID() {
            return {
                file_name: this.file_name,
                name: this.name,
            };
        },
    },
    actions: {
        updateID(file_name: string, name: string) {
            this.file_name = file_name;
            this.name = name;
        },
    },
});
