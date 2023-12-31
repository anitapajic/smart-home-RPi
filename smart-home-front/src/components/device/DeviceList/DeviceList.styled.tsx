import styled from "styled-components";

export const ItemsListStyle = styled.div`
  margin-top: 50px;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: space-around;

  @media (max-width: 768px) {
    gap: 8px;
  }
`;