import { render, screen, fireEvent } from '@testing-library/react';
import Test from './Test';

test('artist added when add button clicked', () => {
  render(<Test />);
  const button = screen.getByText("Add an artist");
  const textInput = screen.getByTestId("text-input");
  fireEvent.change(textInput, {target: {value: "BTOB"}});
  fireEvent.click(button);

  expect(button).toBeInTheDocument();

  const newArtist = screen.queryByText("BTOB");
  expect(newArtist).toBeInTheDocument();
});

test('artist delete button clicked', () => {
  render(<Test />);
  const button = screen.getByText("Delete an artist");
  const textInput = screen.getByTestId("text-input");
  fireEvent.change(textInput, {target: {value: "BTOB"}});
  fireEvent.click(button);

  expect(button).toBeInTheDocument();

  const newArtist = screen.queryByText("BTOB");
  expect(newArtist).toBeInTheDocument();
});

test('save button was clicked', () =>{
  render(<Test />);
  const button = screen.getByText("Save!");
  fireEvent.click(button);

  expect(button).toBeInTheDocument();
});