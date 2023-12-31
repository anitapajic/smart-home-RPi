import { ButtonStyled } from "./Button.styled";


export type ButtonProps = {
    text: string
    onClickHandler?: () => void;
}
export default function Button({text, onClickHandler }: ButtonProps) {
    return (
        <ButtonStyled onClick={onClickHandler}>
                <p>{text}</p> 
        </ButtonStyled>
    )
}