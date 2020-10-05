
<template>
    <div>
       <a class="btn btn-primary">{{ msg }}</a>
    </div>

</template>

<script>
    import axios from 'axios'

    export default{

        name:'Ping',
        data(){
            return {
                msg:''
            }
        },

        methods: {
            getMessage(){
                const path = 'http://localhost:5000/api/ping'
                axios.get(path)
                .then((res)=>{
                    this.msg=res.data;
                })
                .catch((error)=>{
                    console.log(error);
                })
                }
            
        },
        created(){
            this.getMessage()
        }
    }

</script>

