import styled from "styled-components";



export const Form = styled.form`
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 15px;
  padding: 0 20px;
  height: 100%;
  text-align: center;
`;
export const CustomInput = styled.input`
  background-color: #eee;
  margin: 5px;
  border: 1px solid ${({ theme }) => theme.colors.main};
  padding-left: 15px;
  padding-right: 15px;
  padding-top:20px;
  padding-bottom: 13px;
  border-radius: 7px;
width: 100%;
 &.invalidInput {
    border: 1px solid red;
  }
  &:focus + label,
  &:not(:placeholder-shown) + label {
    top: 5px;
    font-size: 12px;
    color: #888;
  }
`;
