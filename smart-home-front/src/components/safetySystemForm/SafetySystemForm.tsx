import { useState } from "react";
import { showToast } from "../shared/toast/CustomToast";
import { CustomInput, Form } from "./SafetySystem.styled";
import Service from "../../services/Service";
import { ButtonStyled } from "../shared/button/Button.styled";

export type SafetySystemFormProps = {
    onSubmit: () => void;
};

export default function SafetySystemForm({ onSubmit }: SafetySystemFormProps) {

    const [pin, setPin] = useState("")
    const [isPinValid, setIsPinValid] = useState(false);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setPin(value);
        setIsPinValid(!(value.length < 4));
        if(value.length > 4){
            setPin("")
        }
    }



    const handleDecline = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        if(isPinValid){
            Service.setSafetySystem(pin).then(response => {
                console.log(response.data)
                onSubmit()
            }).catch(error => {
                console.error("Error: ", error)
            })
        }
    }


    return <Form>

        <CustomInput
            type="text"
            placeholder="Pin"
            name="pin"
            value={pin}
            onChange={handleInputChange}
        />
        {isPinValid ? null : (
            <small className="error-text">Enter 4 numbers!</small>
        )}
        {isPinValid && (
            <ButtonStyled onClick={handleDecline}>Set</ButtonStyled>
        )}
    </Form>

}

