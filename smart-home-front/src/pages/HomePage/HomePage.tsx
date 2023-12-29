import { StyledPage } from "../../components/shared/styled/SharedStyles.styled"
import houseMapImage from '../../house-map.png';
import { ImageStyle } from "./HomePage.styled";

export default function HomePage() {
    return (
        <>
            <StyledPage>
                <ImageStyle src={houseMapImage} alt="House Map" />
            </StyledPage>
        </>
    )
}