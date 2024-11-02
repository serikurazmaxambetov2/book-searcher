import { ApiProperty } from '@nestjs/swagger';
import { IsString } from 'class-validator';

export class BookCreateDto {
  @IsString({ message: 'validation.IS_STRING' })
  @ApiProperty({ type: 'string' })
  title: string;

  @IsString({ message: 'validation.IS_STRING' })
  @ApiProperty({ type: 'string' })
  description: string;
}
