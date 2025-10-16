import { StatusBar } from "expo-status-bar";
import { Text, View } from "react-native"; // Standard RN components
import { styled } from "nativewind"; // <-- Import styled

// Create styled components for Tailwind usage
const StyledView = styled(View);
const StyledText = styled(Text);

export default function App() {
  return (
    <StyledView className="flex-1 items-center justify-center bg-blue-900">
      <StyledText className="text-3xl font-bold text-white">
        ZIP Mobile App is Ready!
      </StyledText>
      <StatusBar style="auto" />
    </StyledView>
  );
}
