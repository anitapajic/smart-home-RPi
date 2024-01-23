import customAxios from "./AxiosInterceptor/AxiosInterceptor";


class Service{  
    
    setSafetySystem(pin : string) {
        return customAxios.put(`/safety_system/${pin}`);
    }

    deactivateAlarm(pin : string) {
        return customAxios.put(`/deactivate_alarm/${pin}`);
    }

    setAlarmClock(time : string) {
        return customAxios.put(`/set_alarm_clock/${time}`);
    }

    turnOffAlarmClock() {
        return customAxios.get(`/deactivate_alarm_clock`);
    }

}

export default new Service();