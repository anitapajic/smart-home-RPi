import { useState } from "react";
import { CustomInput, Form } from "../safetySystemForm/SafetySystem.styled";
import { ButtonStyled } from "../shared/button/Button.styled";

export type AlarmClockFormProps = {
    isClockOn: boolean;
    onSubmit: (time?: string) => void;
};

export default function AlarmClockForm({ isClockOn, onSubmit }: AlarmClockFormProps) {
    const [time, setTime] = useState("");

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setTime(value);
    }

    const handleSubmit = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        onSubmit(time);
        setTime('');
    }

    const handleDecline = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        onSubmit();

    }

    return (
        <Form>
            {isClockOn ? (
                <>
                    <h2>YOUR ALARM CLOCK IS ON</h2>
                    <ButtonStyled onClick={handleDecline}>Turn off</ButtonStyled>
                </>

            ) : (
                <>
                    <CustomInput
                        type="datetime-local"
                        placeholder="Date and time"
                        name="datetime"
                        value={time}
                        onChange={handleInputChange}
                    />
                    <ButtonStyled onClick={handleSubmit}>Set</ButtonStyled>

                </>
            )}

        </Form>
    );
}