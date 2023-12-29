import styled from "styled-components";

export const Card = styled.article`
  width: 200px;
  padding: 20px;
  position: relative;
  border: 4px solid ${({ theme }) => theme.colors.main};
  margin: 20px;
  text-align: center;
  background-color: ${({ theme }) => theme.colors.secondColor};
  h3 {
    margin-right: 3px;
    color: ${({ theme }) => theme.colors.textColor};
    font-size: 20px;
  }
  h1{
    color: ${({ theme }) => theme.colors.textColor};
  }

  &:hover {
    border: 4px solid ${({ theme }) => theme.colors.textColor};
    cursor: pointer;
  }
  border-radius: 20px;
`;