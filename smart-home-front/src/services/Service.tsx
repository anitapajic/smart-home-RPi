import customAxios from "./AxiosInterceptor/AxiosInterceptor";


class Service{  
    
    setSafetySystem(pin : string) {
        console.log("sojidocjweocj")
        return customAxios.put(`/safety_system/${pin}`);
    }

}

export default new Service();