<template>
    <div>
        <h3>做一个简单的搜索框</h3>
        <input type="text" v-model="name">
        <span><button @click="search()">搜索</button></span>     
        <div>{{req}}</div>   
    </div>
</template>

<script>
    export default {
        data() {
            return {
                name:"",
                req:{}
            }
        },
        methods:{
            search(){
                this.$http.get("/api/search_sings?Name="+this.name).then(                    
                    (data)=>{
                        this.req=JSON.stringify(data.data)
                    }
                )
            }
        }
    }
</script>

<style lang="scss" scoped>

</style>