import { useState } from "react";
import { showToast } from "../shared/toast/CustomToast";
import { CustomInput, Form } from "./SafetySystem.styled";
import Service from "../../services/Service";
import { ButtonStyled } from "../shared/button/Button.styled";

export type SafetySystemFormProps = {
    isAlarm: boolean
    onSubmit: (pin: string) => void;
};

export default function SafetySystemForm({ isAlarm, onSubmit }: SafetySystemFormProps) {

    const [pin, setPin] = useState("")
    const [resp, setResp] = useState(true)
    const [isPinValid, setIsPinValid] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setPin(value);
        setIsPinValid(!(value.length < 4));
        if (value.length > 4) {
            setPin("")
        }
    }



    const handleDecline = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();

        if (isPinValid) {
            onSubmit(pin)
            setPin('')
            setIsLoading(true);

            setTimeout(async () => {
                setIsLoading(false)
                setResp(false)
            }, 5000);

        }
    }


    return <Form>
        {isLoading ? (


            <iframe
                src="https://giphy.com/embed/JFTg9PBtHZz9hHRkBN"
                width="100%"
                height="100%"
                frameBorder="0"
            ></iframe>

        ) : (
            <>
                {isAlarm ? (
                    <>
                        {!resp ? (
                            <h2>Wrong pin, try again</h2>
                        ) : (
                            <h2>Enter pin</h2>
                        )}
                    </>
                ) : (
                    <h2>Enter new pin</h2>
                )}

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
            </>
        )

        }


    </Form>

}

