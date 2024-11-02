import { ApiProperty } from '@nestjs/swagger';
import { Transform } from 'class-transformer';
import { IsNumber } from 'class-validator';

export class BookFilterDto {
  @IsNumber({}, { message: 'validation.IS_NUMBER' })
  @ApiProperty({ type: 'number' })
  @Transform(({ value }) => +value)
  id: number;
}
