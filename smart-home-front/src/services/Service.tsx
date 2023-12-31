import customAxios from "./AxiosInterceptor/AxiosInterceptor";


class Service{  
    
    setSafetySystem(pin : string) {
        return customAxios.put(`/safety_system/${pin}`);
    }

    deactivateAlarm(pin : string) {
        return customAxios.put(`/deactivate_alarm/${pin}`);
    }

}

export default new Service();