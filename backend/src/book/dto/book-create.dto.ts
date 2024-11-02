import { IsString } from 'class-validator';

export class BookCreateDto {
  @IsString({ message: 'validation.IS_STRING' })
  title: string;

  @IsString({ message: 'validation.IS_STRING' })
  description: string;
}
